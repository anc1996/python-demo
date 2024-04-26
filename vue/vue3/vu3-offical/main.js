const app = Vue.createApp({
    data() {
        return {
            cart: [],
            // 用户可以添加任何他们想要的商品到购物车中。
            premium: true
        }
    },
    methods: {
        updateCart(id) {
            this.cart.push(id)
        },
        removeById(id) {
            // 它接受一个参数 id，并用于从某个数组中移除具有特定 id 的元素。这个函数是在一个名为 Cart 的类中定义的，该类有一个名为 cart 的属性，表示购物车中的物品列表。
            const index = this.cart.indexOf(id)
            if(index>-1){
            this.cart.splice(index,1)
            }
        }
     }
})