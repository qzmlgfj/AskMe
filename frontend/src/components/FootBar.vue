<template>
    <div class="foot-bar">
        <n-p>
            Designed by Ant
        </n-p>
    </div>
</template>

<script>
import { NP } from "naive-ui";
export default {
    name: 'FooterBar',
    components: {
        NP
    }
}
</script>

<style scoped>
.foot-bar {
    display: flex;
    box-sizing: border-box;
    height: 100%;
    align-items: center;
    justify-content: center;
    padding: 0 2vw;
}
</style>
