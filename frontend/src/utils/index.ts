/**
 * local環境かの判断
 *
 * @export
 * @returns {boolean}
 */
export function isLocal(): boolean {
  return import.meta.env.VITE_APP_ENV === 'local'
}

/**
 * development環境かの判断
 *
 * @export
 * @returns {boolean}
 */
export function isDevelopment(): boolean {
  return import.meta.env.VITE_APP_ENV === 'development'
}

/**
 * staging環境かの判断
 *
 * @export
 * @returns {boolean}
 */
export function isStaging(): boolean {
  return import.meta.env.VITE_APP_ENV === 'staging'
}

/**
 * production環境かの判断
 *
 * @export
 * @returns {boolean}
 */
export function isProduction(): boolean {
  return import.meta.env.VITE_APP_ENV === 'production'
}
