module.exports = {
  devServer: {
    disableHostCheck: true
  },
  outputDir: '../docs/',
  publicPath: process.env.NODE_ENV === 'production'
    ? '/crypto_dashboard/'
    : '/'
}
