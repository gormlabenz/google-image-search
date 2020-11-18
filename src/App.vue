<template>
  <div>
    <div class=" text-center m-8">
      <button
        class="border-red-600 bg-white border-2 px-4 py-2 rounded-lg text-gray-800 font-bold shadow-md"
        v-bind:class="{ 'bg-red-600 text-gray-100': isActive }"
        @click="sendMessage"
      >
        Record
      </button>
    </div>
    <div class="w-screen h-screen flex flex-wrap">
      <div v-for="url in urls" :key="url" class="w-1/4 p-4">
        <img class="object-cover" :src="url" alt="" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      urls: [
        "https://www.himgs.com/imagenes/hello/social/hello-fb-logo.png",
        "https://cdn.britannica.com/98/898-050-FABCB62A/Germany.jpg",
        "https://i.ytimg.com/vi/8aShfolR6w8/maxresdefault.jpg",
        "https://i.ytimg.com/vi/L4D-orTkaLc/maxresdefault.jpg",
        "https://cdn57.androidauthority.net/wp-content/uploads/2020/04/Google-Play-Store-on-smartphone-stock-photo-2-920x470.jpg",
        "https://images-na.ssl-images-amazon.com/images/I/41jIw1mUV4L._AC_.jpg",
      ],
      isActive: false,
    };
  },
  sockets: {
    connect: function() {
      console.log("socket connected");
    },
    serverToClient: function(urls) {
      console.log(urls);
      this.urls = urls;
      this.isActive = false;
    },
  },
  methods: {
    sendMessage() {
      this.$socket.emit("clientToServer", "record");
      this.isActive = true;
    },
  },
};
</script>
