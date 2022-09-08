<template>
    <div class="head-bar">
        <n-h1>AskMe !</n-h1>
    </div>
</template>

<script>
import { NH1 } from "naive-ui";


export default {
    name: 'HeadBar',
    components: {
        NH1
    }
}
</script>

<style scoped>
.head-bar {
    display: flex;
    height: 100%;
    align-items: center;
    padding: 0 2vw;
}

h1 {
    margin: 0;
    padding: 0;
}
</style>
