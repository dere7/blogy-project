import Link from "next/link";
import { useEffect, useReducer, useState } from "react";
import { FaSignOutAlt, FaUser } from "react-icons/fa";
import { Navbar, Container, Loader } from "react-bulma-components";

export default function Nav() {
  const [show, toggle] = useReducer((state) => !state, false)
  const [loggedIn, setLoggedIn] = useState(false)
  const [user, setUser] = useState(null)

  useEffect(() => {
    let token = localStorage.getItem('token')
    if (token) {
      setLoggedIn(true)
      fetch('http://localhost:5000/user/me', {
        headers: {
          'Authorization': 'Bearer ' + token
        }
      }).then(res => res.json()).then(setUser).catch(console.error)
    }
  }, [])

  const handleLogout = () => {
    toggle()
    setLoggedIn(false)
    localStorage.removeItem('token')
  }
  return (
    <Navbar>
      <Container className="is-flex is-justify-content-space-between">
        <div className="navbar-brand">
          <Link href="/">
            <a className="navbar-item title is-4 m-0">
              Blogy
            </a>
          </Link>
        </div>
        <div>
          <div className="navbar-end">
            <div className="navbar-item">
              {loggedIn ?
                (
                  user ?
                    (
                      <>
                        <p className="mr-4"> Welcome, <b>{user.full_name}</b></p>
                        <div className={"dropdown is-right" + (show ? " is-active" : "")}>
                          <div className="dropdown-trigger">
                            <img className="is-rounded" onClick={toggle} src="/128x128.png" style={{ maxHeight: 48, borderRadius: '50%' }} />
                          </div>
                          <div className="dropdown-menu" role="menu">
                            <div className="dropdown-content">
                              <a href="#" className="dropdown-item">
                                <FaUser className="mr-2" /> Account Dashboard
                              </a>
                              <a className="dropdown-item" onClick={handleLogout}>
                                <FaSignOutAlt className="mr-2" /> Logout
                              </a>
                            </div>
                          </div>
                        </div>
                      </>

                    ) : (<Loader textSize={3} color='primary' />)
                ) : (
                  <div className="buttons">
                    <Link href={'/auth/login'}>
                      <button className="button is-ghost">
                        Log in
                      </button>
                    </Link>
                    <Link href="/auth/signup">
                      <button className="button is-outlined is-primary">
                        <strong>Sign up</strong>
                      </button>
                    </Link>
                  </div>
                )}
            </div>
          </div>
        </div>
      </Container>
    </Navbar >
  )
}