<template>
    <div class="head-bar">
        <n-popover trigger="hover" @update:show="handleTitleUpdateShow">
            <template #trigger>
                <n-h1>AskMe !</n-h1>
            </template>
            <n-text>{{ poetry }}</n-text>
        </n-popover>
        <div style="min-width: 20%; display: flex;" v-if="!ifLogin && !isMobile">
            <n-input v-model:value="questionId" round placeholder="请输入问题ID" autosize clearable style="min-width: 90%" />
            <n-button quaternary circle @click="handleSearch">
                <template #icon>
                    <n-icon>
                        <search />
                    </n-icon>
                </template>
            </n-button>
        </div>
        <n-space :size="isMobile ? 'small' : 'medium'">
            <n-popover v-if="isMobile" trigger="click" @update:show="handleTitleUpdateShow">
                <template #trigger>
                    <n-button quaternary :size="isMobile ? 'medium' : 'large'">
                        <template #icon>
                            <n-icon>
                                <search />
                            </n-icon>
                        </template>
                        <template v-if="!isMobile">搜索</template>
                    </n-button>
                </template>
                <n-input v-model:value="questionId" round placeholder="请输入问题ID" clearable @keyup="handleKeyUp"/>
            </n-popover>
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
            <n-button quaternary :size="isMobile ? 'medium' : 'large'" tag="a" href="https://github.com/qzmlgfj/AskMe"
                v-if="!ifLogin">
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
import { inject, computed, ref } from "vue";
import { NH1, NPopover, NText, NSpace, NButton, NIcon, NBadge, NInput } from "naive-ui";
import { Mail, MailForward, MailOpened, Refresh, BrandGithub, Sun, Moon, Search } from "@vicons/tabler";
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
        NInput,
        Mail,
        MailForward,
        MailOpened,
        Refresh,
        BrandGithub,
        Sun,
        Moon,
        Search
    },
    setup() {
        const { isDaytime, switchTheme } = inject("switchTheme");
        const theme = computed(() => isDaytime.value ? "深色" : "浅色");

        const store = useStore();
        const isMobile = computed(() => store.state.isMobile);
        const queryMode = computed(() => store.state.queryMode);
        const ifLogin = computed(() => store.state.userName != "");
        const unansweredNum = computed(() => store.state.unansweredNum);

        const questionId = ref(null);

        const handleSearch = () => {
            store.commit("setQueryMode", "get_question/" + questionId.value);
            store.commit("updateQuestion");
        }

        return {
            isDaytime,
            theme,
            switchTheme,
            isMobile,
            queryMode,
            ifLogin,
            unansweredNum,
            questionId,
            handleSearch
        }
    },
    data() {
        return {
            poetry: "",
            queryText: "未回复"
        }
    },
    methods: {
        handleTitleUpdateShow(show) {
            if (!show) {
                jinrishici.load(result => {
                    this.poetry = result.data.content;
                });
            }
        },
        handleKeyUp(event) {
            if (event.code == "enter") {
                this.handleSearch();
            }
        },
        handleRefresh() {
            this.$store.commit("updateQuestion");
        },
        handleFilter() {
            if (this.$store.state.queryMode == "admin_answered") {
                this.$store.commit("setQueryMode", "all");
                this.queryText = "全部";
            } else if (this.$store.state.queryMode === "all") {
                this.$store.commit("setQueryMode", "unanswered");
                this.queryText = "未回复";
            } else {
                this.$store.commit("setQueryMode", "admin_answered");
                this.queryText = "已回复";
            }
            this.$store.commit("updateQuestion");
        }
    },
    created() {
        jinrishici.load(result => {
            this.poetry = result.data.content;
        });
    },
    watch: {
        questionId: {
            handler: function (val) {
                if (val == "") {
                    this.$store.commit("setQueryMode", "unprivate_and_answered");
                    this.$store.commit("updateQuestion");
                }
            }
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
