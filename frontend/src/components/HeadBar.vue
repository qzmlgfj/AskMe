<template>
    <div class="head-bar">
        <n-popover trigger="hover" @update:show="handleUpdateShow">
            <template #trigger>
                <n-h1>AskMe !</n-h1>
            </template>
            <n-text>{{ poetry }}</n-text>
        </n-popover>
        <n-space :size="isMobile ? 'small' : 'medium'">
            <n-badge :value="unansweredNum" type="success" v-if="ifLogin">
                <n-button quaternary @click="handleFilter" :size="isMobile ? 'medium' : 'large'">
                    <template #icon>
                        <n-icon>
                            <mail-opened v-if="queryMode == 'answered'" />
                            <mail-forward v-else-if="queryMode == 'unanswered'" />
                            <mail v-else />
                        </n-icon>
                    </template>
                    <template v-if="!isMobile">{{ queryText }}</template>
                </n-button>
            </n-badge>
            <n-button quaternary @click="handleRefresh" :size="isMobile ? 'medium' : 'large'">
                <template #icon>
                    <n-icon>
                        <refresh />
                    </n-icon>
                </template>
                <template v-if="!isMobile">刷新</template>
            </n-button>
            <n-button quaternary @click="switchTheme" :size="isMobile ? 'medium' : 'large'">
                <template #icon>
                    <n-icon>
                        <sun v-if="isDaytime" />
                        <moon v-else />
                    </n-icon>
                </template>
                <template v-if="!isMobile">{{ theme }}</template>
            </n-button>
            <n-button quaternary :size="isMobile ? 'medium' : 'large'" tag="a" href="https://github.com/qzmlgfj/AskMe" v-if="!ifLogin">
                <template #icon>
                    <n-icon>
                        <brand-github />
                    </n-icon>
                </template>
                <template v-if="!isMobile">GitHub</template>
            </n-button>
        </n-space>
    </div>
</template>

<script>
import { inject, computed } from "vue";
import { NH1, NPopover, NText, NSpace, NButton, NIcon, NBadge } from "naive-ui";
import { Mail, MailForward, MailOpened, Refresh, BrandGithub, Sun, Moon } from "@vicons/tabler";
import { useStore } from "vuex";

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
        NBadge,
        Mail,
        MailForward,
        MailOpened,
        Refresh,
        BrandGithub,
        Sun,
        Moon
    },
    setup() {
        const { isDaytime, switchTheme } = inject("switchTheme");
        const theme = computed(() => isDaytime.value ? "深色" : "浅色");

        const store = useStore();
        const isMobile = computed(() => store.state.isMobile);
        const queryMode = computed(() => store.state.queryMode);
        const ifLogin = computed(() => store.state.userName != "");
        const unansweredNum = computed(() => store.state.unansweredNum);

        return {
            isDaytime,
            theme,
            switchTheme,
            isMobile,
            queryMode,
            ifLogin,
            unansweredNum,
        }
    },
    data() {
        return {
            poetry: "",
            queryText: "已回复"
        }
    },
    methods: {
        handleUpdateShow(show) {
            if (!show) {
                jinrishici.load(result => {
                    this.poetry = result.data.content;
                });
            }
        },
        handleRefresh() {
            this.$store.commit("updateQuestion");
        },
        handleFilter() {
            if (this.$store.state.queryMode == "answered") {
                this.$store.commit("setQueryMode", "all");
                this.queryText = "全部";
            } else if (this.$store.state.queryMode === "all") {
                this.$store.commit("setQueryMode", "unanswered");
                this.queryText = "未回复";
            } else {
                this.$store.commit("setQueryMode", "answered");
                this.queryText = "已回复";
            }
            this.$store.commit("updateQuestion");
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
