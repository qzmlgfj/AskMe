<template>
    <n-config-provider :theme="naiveTheme">

        <n-layout>
            <div id="container">
                <n-layout-header bordered>
                    <head-bar></head-bar>
                </n-layout-header>
                <n-scrollbar style="max-height: 90vh;">
                    <n-layout-content>
                        <n-message-provider>
                            <main-content></main-content>
                        </n-message-provider>
                    </n-layout-content>
                    <n-layout-footer bordered>
                        <foot-bar></foot-bar>
                    </n-layout-footer>
                </n-scrollbar>
                <n-button id="add-btn" circle strong type="info" size="large" @click="showModal = true">
                    <template #icon>
                        <playlist-add></playlist-add>
                    </template>
                </n-button>
                <n-message-provider>
                    <n-modal v-model:show="showModal">
                        <modal-card></modal-card>
                    </n-modal>
                </n-message-provider>
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
    darkTheme,
    NButton,
    NMessageProvider,
    NModal
} from "naive-ui";

import { PlaylistAdd } from "@vicons/tabler";

import ModalCard from "./components/Cards/ModalCard.vue";
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
        NButton,
        PlaylistAdd,
        NMessageProvider,
        NModal,
        ModalCard,
        HeadBar,
        MainContent,
        FootBar
    },
    setup() {
        const isDaytime = ref(true);
        const naiveTheme = computed(() => isDaytime.value ? {} : darkTheme);
        const showModal = ref(false);

        const switchTheme = () => {
            isDaytime.value = !isDaytime.value;
        };

        const closeModal = () => {
            showModal.value = false;
        };

        provide("switchTheme", {
            isDaytime,
            switchTheme,
        })

        provide("closeModal", {
            closeModal
        })

        return {
            isDaytime,
            naiveTheme,
            showModal,
            closeModal
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
    position: relative;
}

.n-layout-header {
    height: 10vh;
}

.n-layout-footer {
    height: 10vh;
}

#add-btn {
    position: absolute;
    right: 32px;
    bottom: 32px;
}
</style>
