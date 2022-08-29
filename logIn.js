const HOST = ''
const logInForm = document.getElementById('logIn')

class LogInHandler {
    static loginRoute = `${HOST}/user/login`

    static logIn() {
        window.alert('Logged In Successfully')
        window.open('welcome.html')
        window.close()
    }

    static async getAuthToken(user) {
        let res = {
            api_key: ''
        }

        try {
            res = await LogInHandler.postData(user)
            document.cookie = `api_key=${res.api_key}`
            LogInHandler.logIn()
        } catch (e) {
            console.error(e)
        }
    }

    static async postData(data = {}) {
        const url = LogInHandler.loginRoute

        const response = await fetch(url, {
            method: 'POST', mode: 'cors', cache: 'no-cache', credentials: 'same-origin', headers: {
                'Content-Type': 'application/json'
            }, redirect: 'follow', referrerPolicy: 'no-referrer', body: JSON.stringify(data)
        })

        return response.json()
    }
}

class FormHandler {
    static handleLogInSubmitEvt(evt) {
        evt.preventDefault()
        const formElements = logInForm.elements

        const email = formElements['email'].value
        const password = formElements['password'].value

        LogInHandler.getAuthToken({email, password}).then()
    }
}

logInForm.onsubmit = FormHandler.handleLogInSubmitEvt
