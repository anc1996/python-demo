app.component('review-form', {
    template:
    /*html*/`
    <!--@submit.prevent 事件监听器：这是一个事件监听器，当表单提交时会阻止默认行为。
    submit 是事件类型，prevent 是一个修饰符，表示阻止事件冒泡。-->
    <form class="review-form" @submit.prevent="onSubmit">
    <h3>Leave a review</h3>
    
    <label for="name">Name:</label>
    <!--，v-model将HTML输入元素的值与Vue实例的属性进行双向绑定。-->
    <input id="name" v-model="name" />

    <label for="review">Review:</label>      
    <textarea id="review" v-model="review"></textarea>

    <label for="rating">Rating:</label>
    <!--用于将HTML中的表单元素（如<select>）与Vue实例的数据属性进行双向绑定。-->
    <select id="rating" v-model.number="rating">
      <option>5</option>
      <option>4</option>
      <option>3</option>
      <option>2</option>
      <option>1</option>
    </select>
    
   <!-- solution -->
    <label for="recommend">Would you recommend this product?</label>
    <select id="recommend" v-model="recommend">
      <option>Yes</option>
      <option>No</option>
    </select>
    <!-- solution --> 
    

    <input class="button" type="submit" value="Submit">
  </form>`,
    data(){
        return{
            name: '',
            review: '',
            rating: null,
            recommend: null
        }
    },
    methods:{
        onSubmit(){
            if(this.name == '' || this.review == '' || this.rating == null || this.recommend == null){
                alert('Review form incomplete. Please fill out every field.')
                return
            }
            let productReview = {
                name: this.name,
                review: this.review,
                rating: this.rating,
                recommend:this.recommend
            }
            this.$emit('review-submitted', productReview)
            this.name=''
            this.review=''
            this.rating=null,
            this.recommend=null
        },
    }
})