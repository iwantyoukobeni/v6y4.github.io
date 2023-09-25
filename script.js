<script>
new Vue({
  el: '#app',
  methods: {
    toggleLinks() {
      document.getElementById("links-container").classList.toggle("show-links");
    }
  },
  data: {
    spec: {
      host: "https://www.google.com",
      title: "Google Search",
      description: "Hello, API",
      opened: true,
      request: [{
        method: 'get',    // post, delete or put 
        description: "Google Home",
        url: "/"
      }]
    }
  }
})
</script>



