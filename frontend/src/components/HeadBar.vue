<template>
    <div class="head-bar">
        <n-popover trigger="hover" @update:show="handleTitleUpdateShow">
            <template #trigger>
                <n-h1>AskMe !</n-h1>
            </template>
            <n-text>{{ poetry }}</n-text>
        </n-popover>
        <div v-if="!ifLogin && !isMobile" style="min-width: 20%; display: flex">
            <n-input
                v-model:value="questionId"
                round
                placeholder="请输入问题ID，回车键进行搜索"
                autosize
                clearable
                style="min-width: 90%"
                @keypress="
                    (event) => {
                        if (event.code == 'Enter') handleSearch();
                    }
                "
            />
        </div>
        <n-space :size="isMobile ? 'small' : 'medium'">
            <n-popover
                v-if="isMobile"
                trigger="click"
                @update:show="handleTitleUpdateShow"
            >
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
                <n-input
                    v-model:value="questionId"
                    round
                    placeholder="请输入问题ID"
                    clearable
                    @keypress="
                        (event) => {
                            if (event.code == 'Enter') handleSearch();
                        }
                    "
                />
            </n-popover>
            <n-badge v-if="ifLogin" :value="unansweredNum" type="success">
                <n-button
                    quaternary
                    :size="isMobile ? 'medium' : 'large'"
                    @click="handleFilter"
                >
                    <template #icon>
                        <n-icon>
                            <mail-opened v-if="queryMode == 'admin_answered'" />
                            <mail-forward
                                v-else-if="queryMode == 'unanswered'"
                            />
                            <mail v-else />
                        </n-icon>
                    </template>
                    <template v-if="!isMobile">{{ queryText }}</template>
                </n-button>
            </n-badge>
            <n-button
                quaternary
                :size="isMobile ? 'medium' : 'large'"
                @click="handleRefresh"
            >
                <template #icon>
                    <n-icon>
                        <refresh />
                    </n-icon>
                </template>
                <template v-if="!isMobile">刷新</template>
            </n-button>
            <n-button
                quaternary
                :size="isMobile ? 'medium' : 'large'"
                @click="switchTheme"
            >
                <template #icon>
                    <n-icon>
                        <moon v-if="isDaytime" />
                        <sun v-else />
                    </n-icon>
                </template>
                <template v-if="!isMobile">{{ theme }}</template>
            </n-button>
            <n-button
                v-if="!ifLogin"
                quaternary
                :size="isMobile ? 'medium' : 'large'"
                tag="a"
                href="https://github.com/qzmlgfj/AskMe"
            >
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
import {
    NH1,
    NPopover,
    NText,
    NSpace,
    NButton,
    NIcon,
    NBadge,
    NInput,
} from "naive-ui";
import {
    Mail,
    MailForward,
    MailOpened,
    Refresh,
    BrandGithub,
    Sun,
    Moon,
    Search,
} from "@vicons/tabler";
import { useStore } from "vuex";
import { load } from "jinrishici";

export default {
    name: "HeadBar",
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
        Search,
    },
    setup() {
        const { isDaytime, switchTheme } = inject("switchTheme");
        const theme = computed(() => (isDaytime.value ? "深色" : "浅色"));

        const store = useStore();
        const isMobile = computed(() => store.state.isMobile);
        const queryMode = computed(() => store.state.queryMode);
        const ifLogin = computed(() => store.state.userName != "");
        const unansweredNum = computed(() => store.state.unansweredNum);

        const questionId = ref(null);

        const handleSearch = () => {
            store.commit("setQueryMode", "get_question/" + questionId.value);
            store.commit("updateQuestion");
        };

        return {
            isDaytime,
            theme,
            switchTheme,
            isMobile,
            queryMode,
            ifLogin,
            unansweredNum,
            questionId,
            handleSearch,
        };
    },
    data() {
        return {
            poetry: "",
            queryText: "未回复",
        };
    },
    watch: {
        questionId: {
            handler: function (val) {
                if (val == "") {
                    this.$store.commit(
                        "setQueryMode",
                        "unprivate_and_answered",
                    );
                    this.$store.commit("updateQuestion");
                }
            },
        },
        queryMode: {
            handler: function (val) {
                switch (val) {
                    case "admin_answered":
                        this.queryText = "已回复";
                        break;
                    case "all":
                        this.queryText = "全部";
                        break;
                    case "unanswered":
                        this.queryText = "未回复";
                        break;
                    default:
                        break;
                }
            },
        },
    },
    created() {
        load((result) => {
            this.poetry = result.data.content;
        });
    },
    methods: {
        handleTitleUpdateShow(show) {
            if (!show) {
                load((result) => {
                    this.poetry = result.data.content;
                });
            }
        },
        handleKeyUp(event) {
            if (event.code == "Enter") {
                this.handleSearch();
            }
        },
        handleRefresh() {
            this.$store.commit("updateQuestion");
        },
        handleFilter() {
            if (this.$store.state.queryMode == "admin_answered") {
                this.$store.commit("setQueryMode", "all");
            } else if (this.$store.state.queryMode === "all") {
                this.$store.commit("setQueryMode", "unanswered");
            } else {
                this.$store.commit("setQueryMode", "admin_answered");
            }
            this.$store.commit("updateQuestion");
        },
    },
};
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
