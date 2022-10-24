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
                <n-button id="add-btn" circle strong type="info" size="large" @click="showAddQuestionModal">
                    <template #icon>
                        <playlist-add></playlist-add>
                    </template>
                </n-button>
                <n-message-provider>
                    <n-modal v-model:show="showModal">
                        <card></card>
                    </n-modal>
                </n-message-provider>
            </div>
        </n-layout>
    </n-config-provider>
</template>

<script>
import { ref, computed, provide } from "vue";
import { useStore } from "vuex";

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

import Card from "./components/Card.vue";
import HeadBar from "./components/HeadBar.vue";
import MainContent from "./components/MainContent.vue";
import FootBar from "./components/FootBar.vue";

// import { getCurrentUser } from "@/utils/request";

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
        Card,
        HeadBar,
        MainContent,
        FootBar
    },
    setup() {
        const isDaytime = ref(true);
        const naiveTheme = computed(() => isDaytime.value ? {} : darkTheme);
        const showModal = ref(false);
        const cardName = ref("");
        const store = useStore();

        const switchTheme = () => {
            isDaytime.value = !isDaytime.value;
        };

        const closeModal = () => {
            showModal.value = false;
        };

        const setCardName = (name) => {
            cardName.value = name;
        };

        const showAuthModal = (modalName) => {
            setCardName(modalName);
            showModal.value = true;
        };

        const showAddQuestionModal = () => {
            setCardName("addQuestion");
            showModal.value = true;
        };

        const showAnswerQuestionModal = (id) => {
            store.commit("setCurrentQuestionID", id);
            setCardName("answerQuestion");
            showModal.value = true;
        };

        const showEditQuestionModal = (id) => {
            store.commit("setCurrentQuestionID", id);
            setCardName("modifyQuestion");
            showModal.value = true;
        };

        provide("switchTheme", {
            isDaytime,
            switchTheme,
        })

        provide("closeModal", {
            closeModal
        })

        provide("cardName", {
            cardName
        })

        provide("setCardName", {
            setCardName
        })

        provide("showAuthModal", {
            showAuthModal
        })

        provide("showAnswerQuestionModal", {
            showAnswerQuestionModal
        })

        provide("showEditQuestionModal", {
            showEditQuestionModal
        })

        return {
            isDaytime,
            naiveTheme,
            showModal,
            closeModal,
            cardName,
            setCardName,
            showAddQuestionModal
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
