<template>
    <div class="head-bar">
        <n-popover trigger="hover" @update:show="handleUpdateShow">
            <template #trigger>
                <n-h1>AskMe !</n-h1>
            </template>
            <n-text>{{poetry}}</n-text>
        </n-popover>
        <n-space>
            <n-button quaternary @click="switchTheme" size="large">
                <template #icon>
                    <n-icon>
                        <sun v-if="isDaytime" />
                        <moon v-else />
                    </n-icon>
                </template>
                {{theme}}
            </n-button>
            <n-button quaternary size="large" tag="a" href="https://github.com/qzmlgfj/AskMe">
                <template #icon>
                    <n-icon>
                        <brand-github />
                    </n-icon>
                </template>
                GitHub
            </n-button>
        </n-space>
    </div>
</template>

<script>
import { inject, computed } from "vue";
import { NH1, NPopover, NText, NSpace, NButton, NIcon } from "naive-ui";
import { BrandGithub, Sun, Moon } from "@vicons/tabler";

const jinrishici = require('jinrishici');

export default {
    name: 'HeadBar',
    components: {
        NH1,
        NPopover,
        NText,
        NSpace,
        NButton,
        NIcon,
        BrandGithub,
        Sun,
        Moon
    },
    setup() {
        const { isDaytime, switchTheme } = inject("switchTheme");
        const theme = computed(() => isDaytime.value ? "深色" : "浅色");

        return {
            isDaytime,
            theme,
            switchTheme
        }
    },
    data() {
        return {
            poetry: ""
        }
    },
    methods: {
        handleUpdateShow(show) {
            if (!show) {
                jinrishici.load(result => {
                    this.poetry = result.data.content;
                });
            }
        }
    },
    created() {
        jinrishici.load(result => {
            this.poetry = result.data.content;
        });
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
