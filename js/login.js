const HOST = 'https://saltpe-backend-assignment-production.up.railway.app'
const logInForm = document.getElementById('logIn')
const errorMessage = document.getElementById('error')

class LogInHandler {
    static loginRoute = `${HOST}/user/login`
    static whoAmIRoute = `${HOST}/user/me`

    static async logIn(accessToken, refreshToken) {
        const user = await LogInHandler.whoAmI(accessToken)

        let username = localStorage.getItem('username')

        if (!username || username !== user.username) {
            localStorage.setItem('username', user.username)
        }

        localStorage.setItem('accessToken', user.token)
        localStorage.setItem('refreshToken', refreshToken)

        console.log(localStorage.getItem('username'), localStorage.getItem('accessToken'))


        window.open('welcome.html')
        window.close()
    }

    static async getAuthToken(user) {
        let res = {
            access_token: '', refresh_token: ''
        }

        try {

            res = await LogInHandler.postData(user)
 
            if(!res.detail)
            {
                await LogInHandler.logIn(res.access_token, res.refresh_token)
            }
            
        } catch (e) {
            console.error(e)
            errorMessage.removeAttribute('hidden')
        }
    }

    static async postData(data = {}) {
        const url = LogInHandler.loginRoute

        const myHeaders = new Headers();
        myHeaders.append('Content-Type', 'application/json');

        const myInit = {
            method: 'POST',
            mode: 'cors',
            cache: 'default',
            credentials: 'same-origin',
            headers: myHeaders,
            body: JSON.stringify(data)
        };

        const response = await fetch(url, myInit)


        if (response.status !=200)
        {
            window.alert((await response.json()).detail)
        }

        return await response.json()
    }

    static async whoAmI(accessToken) {
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

        const user = await fetch(LogInHandler.whoAmIRoute, myInit)
        return user.json()
    }
}

class LoginFormHandler {
    static handleLogInSubmitEvt(evt) {
        evt.preventDefault()
        const formElements = logInForm.elements

        const email = formElements['email'].value
        const password = formElements['password'].value

        LogInHandler.getAuthToken({email, password}).then()
        
    }
}

logInForm.onsubmit = LoginFormHandler.handleLogInSubmitEvt
