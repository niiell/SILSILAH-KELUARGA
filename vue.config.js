module.exports = {
  chainWebpack: config => {
    config.module
      .rule('images')
      .test(/\.(png|jpe?g|gif|webp)(\\?.*)?$/)
      .exclude.add(/family_tree_landscape\.png$/)
      .end()
  }
}
