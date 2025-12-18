/**
 * Apilage AI Video Generator SDK
 * JavaScript/TypeScript SDK for generating educational videos
 * 
 * @version 1.0.0
 * @author Apilage AI
 * @license MIT
 */

(function(global, factory) {
    // UMD (Universal Module Definition)
    if (typeof exports === 'object' && typeof module !== 'undefined') {
        // CommonJS
        module.exports = factory();
    } else if (typeof define === 'function' && define.amd) {
        // AMD
        define(factory);
    } else {
        // Browser globals
        global.ApilageAI = factory();
    }
}(typeof self !== 'undefined' ? self : this, function() {
    'use strict';

    /**
     * ApilageAI Video Generator Client
     */
    class ApilageAI {
        /**
         * Create a new ApilageAI client
         * @param {Object} options - Configuration options
         * @param {string} options.baseUrl - API base URL (default: https://gen.apilageai.lk)
         * @param {number} options.pollInterval - Status polling interval in ms (default: 3000)
         * @param {number} options.timeout - Request timeout in ms (default: 30000)
         */
        constructor(options = {}) {
            this.baseUrl = (options.baseUrl || 'https://gen.apilageai.lk').replace(/\/$/, '');
            this.pollInterval = options.pollInterval || 3000;
            this.timeout = options.timeout || 30000;
        }

        /**
         * Make an HTTP request
         * @private
         */
        async _request(method, endpoint, data = null) {
            const url = `${this.baseUrl}${endpoint}`;
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            };

            if (data && (method === 'POST' || method === 'PUT')) {
                options.body = JSON.stringify(data);
            }

            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);
                options.signal = controller.signal;

                const response = await fetch(url, options);
                clearTimeout(timeoutId);

                const json = await response.json();

                if (!response.ok) {
                    throw new ApilageError(
                        json.error || `HTTP ${response.status}`,
                        response.status,
                        json
                    );
                }

                return json;
            } catch (error) {
                if (error.name === 'AbortError') {
                    throw new ApilageError('Request timeout', 408);
                }
                if (error instanceof ApilageError) {
                    throw error;
                }
                throw new ApilageError(error.message, 0);
            }
        }

        /**
         * Submit a video generation request
         * @param {string} topic - Topic to explain in the video
         * @param {Object} options - Generation options
         * @param {string} options.level - Difficulty level: 'basic', 'intermediate', 'special_topic'
         * @returns {Promise<Job>} - Job object with ID and status
         * 
         * @example
         * const job = await client.generate('Explain photosynthesis');
         * console.log(job.id); // 'abc123...'
         */
        async generate(topic, options = {}) {
            const data = {
                topic,
                level: options.level || 'basic'
            };

            const response = await this._request('POST', '/api/generate', data);
            
            return new Job(this, response.job_id, {
                topic,
                level: data.level,
                queuePosition: response.queue_position
            });
        }

        /**
         * Get job status by ID
         * @param {string} jobId - Job ID
         * @returns {Promise<Object>} - Job status object
         */
        async getStatus(jobId) {
            const response = await this._request('GET', `/api/status/${jobId}`);
            return response.job;
        }

        /**
         * Get video details for a completed job
         * @param {string} jobId - Job ID
         * @returns {Promise<Object>} - Video details
         */
        async getVideo(jobId) {
            return await this._request('GET', `/api/video/${jobId}`);
        }

        /**
         * Cancel a pending job
         * @param {string} jobId - Job ID
         * @returns {Promise<Object>} - Cancellation result
         */
        async cancelJob(jobId) {
            return await this._request('POST', `/api/cancel/${jobId}`);
        }

        /**
         * Get current queue status
         * @returns {Promise<Object>} - Queue information
         */
        async getQueue() {
            return await this._request('GET', '/api/queue');
        }

        /**
         * Get list of all generated videos
         * @param {Object} options - Pagination options
         * @param {number} options.limit - Max videos to return (default: 50)
         * @param {number} options.offset - Pagination offset (default: 0)
         * @returns {Promise<Object>} - Videos list
         */
        async getVideos(options = {}) {
            const limit = options.limit || 50;
            const offset = options.offset || 0;
            return await this._request('GET', `/api/videos?limit=${limit}&offset=${offset}`);
        }

        /**
         * Health check
         * @returns {Promise<Object>} - Health status
         */
        async health() {
            return await this._request('GET', '/health');
        }

        /**
         * Generate video and wait for completion
         * @param {string} topic - Topic to explain
         * @param {Object} options - Generation options
         * @param {string} options.level - Difficulty level
         * @param {Function} options.onProgress - Progress callback
         * @param {number} options.maxWaitTime - Maximum wait time in ms (default: 600000 = 10 min)
         * @returns {Promise<Object>} - Completed video details
         * 
         * @example
         * const video = await client.generateAndWait('Pythagorean theorem', {
         *     level: 'basic',
         *     onProgress: (status) => console.log(status.progress)
         * });
         * console.log(video.full_url);
         */
        async generateAndWait(topic, options = {}) {
            const job = await this.generate(topic, options);
            return await job.waitForCompletion(options);
        }
    }

    /**
     * Job class representing a video generation job
     */
    class Job {
        constructor(client, id, initialData = {}) {
            this.client = client;
            this.id = id;
            this.topic = initialData.topic;
            this.level = initialData.level;
            this.status = 'pending';
            this.queuePosition = initialData.queuePosition;
            this.progress = 'Waiting in queue...';
            this.videoUrl = null;
            this.fullUrl = null;
            this.error = null;
        }

        /**
         * Refresh job status from server
         * @returns {Promise<Job>} - Updated job
         */
        async refresh() {
            const data = await this.client.getStatus(this.id);
            this.status = data.status;
            this.progress = data.progress || '';
            this.queuePosition = data.queue_position;
            
            if (data.status === 'completed') {
                this.videoUrl = data.video_url;
                this.fullUrl = this.client.baseUrl + data.video_url;
                this.subtitles = data.subtitles;
            }
            
            if (data.status === 'failed') {
                this.error = data.error;
            }
            
            return this;
        }

        /**
         * Check if job is complete
         * @returns {boolean}
         */
        isComplete() {
            return this.status === 'completed' || this.status === 'failed';
        }

        /**
         * Check if job succeeded
         * @returns {boolean}
         */
        isSuccess() {
            return this.status === 'completed';
        }

        /**
         * Cancel this job
         * @returns {Promise<Object>}
         */
        async cancel() {
            return await this.client.cancelJob(this.id);
        }

        /**
         * Wait for job completion
         * @param {Object} options - Wait options
         * @param {Function} options.onProgress - Progress callback
         * @param {number} options.maxWaitTime - Maximum wait time in ms
         * @returns {Promise<Object>} - Video details
         */
        async waitForCompletion(options = {}) {
            const maxWaitTime = options.maxWaitTime || 600000; // 10 minutes
            const onProgress = options.onProgress || (() => {});
            const startTime = Date.now();

            return new Promise((resolve, reject) => {
                const poll = async () => {
                    try {
                        await this.refresh();
                        
                        // Call progress callback
                        onProgress({
                            status: this.status,
                            progress: this.progress,
                            queuePosition: this.queuePosition
                        });

                        if (this.status === 'completed') {
                            resolve({
                                success: true,
                                jobId: this.id,
                                videoUrl: this.videoUrl,
                                fullUrl: this.fullUrl,
                                subtitles: this.subtitles,
                                topic: this.topic
                            });
                            return;
                        }

                        if (this.status === 'failed') {
                            reject(new ApilageError(this.error || 'Video generation failed', 500));
                            return;
                        }

                        // Check timeout
                        if (Date.now() - startTime > maxWaitTime) {
                            reject(new ApilageError('Timeout waiting for video', 408));
                            return;
                        }

                        // Continue polling
                        setTimeout(poll, this.client.pollInterval);
                    } catch (error) {
                        reject(error);
                    }
                };

                poll();
            });
        }
    }

    /**
     * Custom error class for Apilage API errors
     */
    class ApilageError extends Error {
        constructor(message, statusCode, data = null) {
            super(message);
            this.name = 'ApilageError';
            this.statusCode = statusCode;
            this.data = data;
        }
    }

    // Attach classes to main export
    ApilageAI.Job = Job;
    ApilageAI.ApilageError = ApilageError;

    return ApilageAI;
}));
