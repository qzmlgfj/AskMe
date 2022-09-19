<template>
    <div class="foot-bar">
        <n-text depth="3">AskMe! {{version}} · Made by Ant</n-text>
    </div>
</template>

<script>
import { NText } from "naive-ui";


import { getVersion } from "@/utils/request";
export default {
    name: 'FooterBar',
    components: {
        NText
    },
    data() {
        return {
            version: "",
        };
    },
    mounted() {
        getVersion().then((res) => {
            this.version = res.data;
        });
    },
};
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
