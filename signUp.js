const HOST = 'https://f2786ec234e1.ngrok.io'
const signUpForm = document.getElementById('logIn')

class SignUpHandler {
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
            res = await SignUpHandler.postData(user)
            document.cookie = `api_key=${res.api_key}`
            SignUpHandler.logIn()
        } catch (e) {
            console.error(e)
        }
    }

    static async postData(data = {}) {
        const url = SignUpHandler.loginRoute

        const response = await fetch(url, {
            method: 'POST', mode: 'no-cors', cache: 'no-cache', credentials: 'same-origin', headers: {
                'Content-Type': 'application/json'
            }, redirect: 'follow', referrerPolicy: 'no-referrer', body: JSON.stringify(data)
        });
        return response.json();
    }
}

class FormHandler {
    static handleLogInSubmitEvt(evt) {
        evt.preventDefault()
        const formElements = signUpForm.elements
        const user = {}

        user.email = formElements['email']
        user.password = formElements['password']

        SignUpHandler.getAuthToken(user).then()
    }
}

signUpForm.onsubmit = FormHandler.handleLogInSubmitEvt
