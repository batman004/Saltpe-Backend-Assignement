window.addEventListener('load', welcomeUser)

function welcomeUser(_) {
    const welcomeMessage = document.getElementById('welcomeMessage')
    let username = localStorage.getItem('username')

    if (!username) username = ''

    welcomeMessage.innerText = `Welcome ${username}`
}

const HOST = 'https://saltpe-backend-assignment-production.up.railway.app'
const logoutRoute = `${HOST}/user/logout`

const logoutButton = document.getElementById('logout')
logoutButton.addEventListener('click', handleClick)

async function handleClick(_) {
    const user = localStorage.getItem('username')
    const token = localStorage.getItem('accessToken')
    const LOGOUT_MSG = 'logged out'

    if (!(user || token)) {
        openHomePage()
        return false
    }

    try {
        const res = await logout()

        if (res.status !== LOGOUT_MSG) throw 'error logging out'

        clearLocalUser()
        openHomePage()
    } catch (e) {
        console.error(e)
        window.alert('could not log out')
    }
}

function openHomePage() {
    window.open('index.html')
    window.close()
}

function clearLocalUser() {
    localStorage.setItem('username', undefined)
    localStorage.setItem('accessToken', undefined)
    localStorage.setItem('refreshToken', undefined)
    localStorage.setItem('email', undefined)
}

async function logout(data = {}) {
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

    const response = await fetch(logoutRoute, myInit)
    return response.json()
}

