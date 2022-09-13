<template>
    <div class="head-bar">
        <n-h1>AskMe !</n-h1>
        <n-space>
            <n-button quaternary @click="switchTheme" size="large">{{theme}}</n-button>
            <n-button quaternary size="large" tag="a" href="https://github.com/qzmlgfj">GitHub</n-button>
        </n-space>
    </div>
</template>

<script>
import { inject, computed } from "vue";
import { NH1, NSpace, NButton } from "naive-ui";


export default {
    name: 'HeadBar',
    components: {
        NH1,
        NSpace,
        NButton,
    },
    setup() {
        const { isDaytime, switchTheme } = inject("switchTheme");
        const theme = computed(() => isDaytime.value ? "深色" : "浅色");
        return {
            theme,
            switchTheme,
        }
    }
}
</script>

<style scoped>
.head-bar {
    display: flex;
    height: 100%;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
}

h1 {
    margin: 0;
    padding: 0;
}
</style>
