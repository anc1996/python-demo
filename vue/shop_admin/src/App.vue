<template>
  <div id="app">
    <!-- Vue Router 的一部分，用于实现页面导航功能。
    当用户点击不同的路由时，Vue Router 会根据路由配置自动渲染相应的组件，
    并将渲染后的组件显示在 <router-view> 标签所在的位置。 -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
