import { Auth } from "aws-amplify";

export const auth = {

    namespaced: true,
    state: { user: null,
             token:"" },
    mutations: {
        setUser(state, payload) {
            state.token = payload.token;
            state.user = payload.user;
        }
    },
    actions: {
        async logout({ commit }) {(await Auth.currentSession()).getIdToken().getJwtToken()
            commit("setUser", {user: null, token: ""});
            return await Auth.signOut();
        },  data () {
            return {
              authenticated: sessionStorage.getItem('authenticated') === 'true'
            }
            },
        async login({ commit }, { username, password }) {
            try {   
                 await Auth.signIn({
                    username,
                    password
                });

                const userInfo = await Auth.currentUserInfo();
                const Jwt = (await Auth.currentSession()).getIdToken().getJwtToken();
                commit("setUser", {
                    user: userInfo, 
                    token: Jwt
                });
                return Promise.resolve("Success");


            } catch (error) {
                console.log(error);
                return Promise.reject(error);
            }
        },
        async confirmSignUp(_, { username, code }) {
            try {
                await Auth.confirmSignUp(username, code);
                return Promise.resolve();

            } catch (error) {
                console.log(error);
                return Promise.reject(error);

            }
        },
        async signUp(_, { username, password, email, name }) {
            try {
                await Auth.signUp({
                    username,
                    password,
                    attributes: {
                        email,
                        name
                    }
                });
                return Promise.resolve();

            } catch (error) {
                console.log(error);
                return Promise.reject(error);

            }
        },
        async authAction({ commit }) {
            const userInfo = await Auth.currentUserInfo();
            const Jwt = (await Auth.currentSession()).getIdToken().getJwtToken();
            commit("setUser", {
                user: userInfo, 
                token: Jwt
            });

        }

    },
    getters: {
        user: (state) => state.user,
        token: (state)=>state.token

    }

}