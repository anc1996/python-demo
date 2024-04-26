app.component('review-list', {
    props:{
        reviews:{
            type:Array,
            // 这个属性是必需的（required）
            required:true
        }
    },
    template:
    /* html */`
      <div class="review-container">
      <h3>Reviews:</h3>
        <ul>
          <li v-for="(review, index) in reviews" :key="index">
            {{ review.name }} gave this {{ review.rating }} stars
            <br/>
            "{{ review.review }}"
            <br/>
            Recommended:{{ review.recommend }}
          </li>
        </ul>
      </div>
    `,

})