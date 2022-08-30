const HOST = 'https://saltpe-backend-assignment-production.up.railway.app'
const signUpForm = document.getElementById('signUp')
const errorMessage = document.getElementById('error')

class SignUpHandler {
    static signupRoute = `${HOST}/user/signup`
    static loginRoute = `${HOST}/user/login`
    static whoAmIRoute = `${HOST}/user/me`

    static setUser(user) {
        localStorage.setItem('first_name', user.first_name)
        localStorage.setItem('last_name', user.last_name)
        localStorage.setItem('username', user.username)
    }

    static signUp(newUser, accessToken, refreshToken) {
        SignUpHandler.setUser(newUser)

        localStorage.setItem('accessToken', accessToken)
        localStorage.setItem('refreshToken', refreshToken)

        window.open('welcome.html')
        window.close()
    }

    static async getAuthToken(user) {
        const userLoginData = {
            email: user.email, password: user.password
        }
        // login user to get auth tokens
        const res = await SignUpHandler.postData(userLoginData, SignUpHandler.loginRoute)
        return res
    }

    static async createUser(userData) {
        // newUser -> user: str, status: created
        const CREATED = 'created'

        try {
            const res = await SignUpHandler.postData(userData)

            if (res.status !== CREATED) throw `Error: ${JSON.stringify(res.detail)}`

            const {access_token, refresh_token} = await SignUpHandler.getAuthToken(userData)
            await SignUpHandler.signUp(userData, access_token, refresh_token)
        } catch (e) {
            console.error(e)
            errorMessage.removeAttribute('hidden')
        }
    }

    static async postData(data = {}, url = SignUpHandler.signupRoute) {
        const token = localStorage.getItem('accessToken')

        if (!token) throw 'Auth Token not found'

        const myHeaders = new Headers();
        myHeaders.append('Content-Type', 'application/json');
        myHeaders.append('Authorization', `Bearer ${token}`)

        const myInit = {
            method: 'POST',
            mode: 'cors',
            cache: 'default',
            credentials: 'same-origin',
            headers: myHeaders,
            body: JSON.stringify(data)
        };

        const response = await fetch(url, myInit)

        return response.json()
    }

    static async whoAmI(accessToken, url = SignUpHandler.whoAmIRoute) {
        /*
        * user ->
        *   username: str
        *   email: str
        *   token: str
        * */

        const myHeaders = new Headers();
        myHeaders.append('Content-Type', 'application/json');
        myHeaders.append('Authorization', `Bearer ${accessToken}`)

        const myInit = {
            method: 'GET', headers: myHeaders, mode: 'cors', cache: 'default',
        };

        const user = await fetch(url, myInit)
        return user.json()
    }
}

class FormHandler {
    static handleLogInSubmitEvt(evt) {
        evt.preventDefault()
        const formElements = signUpForm.elements
        const user = {}

        user.first_name = formElements['firstName'].value
        user.last_name = formElements['lastName'].value
        user.username = formElements['username'].value
        user.email = formElements['email'].value
        user.password = formElements['password'].value

        SignUpHandler.createUser({...user}).then()
    }
}

signUpForm.onsubmit = FormHandler.handleLogInSubmitEvt
