export default {
  Auth: {
    // REQUIRED - Amazon Cognito Region
    region: process.env.VUE_APP_AWS_COGNITO_REGION,

    // OPTIONAL - Amazon Cognito Federated Identity Pool Region
    // Required only if it's different from Amazon Cognito Region
    // identityPoolRegion: 'XX-XXXX-X',

    // OPTIONAL - Amazon Cognito User Pool ID
    userPoolId: process.env.VUE_APP_USER_POOL_ID,

    // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
    userPoolWebClientId: process.env.VUE_APP_USER_POOL_WEB_CLIENT_ID,

    // OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
    mandatorySignIn: false

    // OPTIONAL - Configuration for cookie storage
    // Note: if the secure flag is set to true, then the cookie transmission requires a secure protocol
    // cookieStorage: {
    // REQUIRED - Cookie domain (only required if cookieStorage is provided)
    // domain: '.yourdomain.com',
    // OPTIONAL - Cookie path
    // path: '/',
    // OPTIONAL - Cookie expiration in days
    // expires: 365,
    // OPTIONAL - See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
    // sameSite: "strict" | "lax",
    // OPTIONAL - Cookie secure flag
    // Either true or false, indicating if the cookie transmission requires a secure protocol (https).
    // secure: true
  },

  // OPTIONAL - customized storage object
  // storage: MyStorage,

  // OPTIONAL - Manually set the authentication flow type. Default is 'USER_SRP_AUTH'
  authenticationFlowType: 'USER_PASSWORD_AUTH',

  // OPTIONAL - Manually set key value pairs that can be passed to Cognito Lambda Triggers
  // clientMetadata: { myCustomKey: 'myCustomValue' },

  // OPTIONAL - Hosted UI configuration
  oauth: {
    domain: process.env.VUE_APP_AUTH_URL,
    scope: ['email', 'openid'],
    redirectSignIn: process.env.VUE_APP_OAUTH_REDIRECT_SIGNIN,
    redirectSignOut: process.env.VUE_APP_OAUTH_REDIRECT_SIGNOUT, // Must match Cognito EXACTLY, e.g. trailing '/' or not.
    responseType: 'code' // 'code' or 'token', note that REFRESH token will only be generated when the responseType is code
  }
}
// You can get the current config object
// const currentConfig = Auth.configure();
