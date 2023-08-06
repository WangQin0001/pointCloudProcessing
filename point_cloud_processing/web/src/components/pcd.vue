<!-- this page to display pointcloud -->
<template lang="">
    <div>
        <div id="webgl">
        </div>
    </div>
</template>
<script>

import { renderer } from "./utils/index.js"; //import render,file index.js defined main render logic
export default {
    mounted() {
        this.init();
    },
    methods: {
        init() {
            document.getElementById('webgl').appendChild(renderer.domElement);//Mount the domelement of renderer to the div whose id is webgl for display
        },
    },
}
</script>


<style lang="">
    
</style>