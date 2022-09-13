<template>
    <n-config-provider :theme="naiveTheme">

        <n-layout>
            <div id="container">
                <n-layout-header bordered>
                    <head-bar></head-bar>
                </n-layout-header>
                <n-scrollbar style="max-height: 90vh;">
                <n-layout-content>
                    <main-content></main-content>
                </n-layout-content>
                <n-layout-footer bordered>
                    <foot-bar></foot-bar>
                </n-layout-footer>
                </n-scrollbar>
            </div>
        </n-layout>
    </n-config-provider>
</template>

<script>
import { ref, computed, provide } from "vue";

import {
    NLayout,
    NConfigProvider,
    NLayoutHeader,
    NLayoutContent,
    NLayoutFooter,
    NScrollbar,
    darkTheme
} from "naive-ui";

import HeadBar from "./components/HeadBar.vue";
import MainContent from "./components/MainContent.vue";
import FootBar from "./components/FootBar.vue";

export default {
    name: 'App',
    components: {
        NLayout,
        NConfigProvider,
        NLayoutHeader,
        NLayoutContent,
        NLayoutFooter,
        NScrollbar,
        HeadBar,
        MainContent,
        FootBar
    },
    setup() {
        const isDaytime = ref(true);
        const naiveTheme = computed(() => isDaytime.value ? {} : darkTheme);

        const switchTheme = () => {
            isDaytime.value = !isDaytime.value;
        };

        provide("switchTheme", {
            isDaytime,
            switchTheme,
        })

        return {
            isDaytime,
            naiveTheme
        }
    }
}
</script>

<style>
body {
    box-sizing: border-box;
    margin: 0;
    font-family: v-sans, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
        "Segoe UI Symbol";
}

#container {
    height: 100vh;
}

.n-layout-header {
    height: 10vh;
}

.n-layout-footer {
    height: 10vh;
}
</style>
