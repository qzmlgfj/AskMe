<template>
    <div class="foot-bar">
        <n-text depth="3" @click="handleClick">AskMe! {{ version }} · Made by Ant</n-text>
    </div>
</template>

<script>
import { NText } from "naive-ui";

import { getVersion, checkAdminExists } from "@/utils/request";
export default {
    name: 'FooterBar',
    components: {
        NText
    },
    data() {
        return {
            version: "",
            clickTimes: 0,
        };
    },
    mounted() {
        getVersion().then((res) => {
            this.version = res.data;
        });
    },
    inject: ["showAuthModal"],
    methods: {
        handleClick() {
            this.clickTimes++;
            const { showAuthModal } = this.showAuthModal;
            if (this.clickTimes == 3) {
                if (this.$store.state.userName == "") {
                    checkAdminExists().then((res) => {
                        if (res.data.status == "no") {
                            showAuthModal("register");
                        } else {
                            showAuthModal("login");
                        }
                    });
                } else {
                    this.$store.commit("clearUserName");
                    this.$store.commit("setQueryMode", "answered");
                    this.$store.commit("updateQuestion");
                }
                this.clickTimes = 0;
            }
        }
    }
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
