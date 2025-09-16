import "./fonts/SanFranciscoProDisplay/fonts.css";
import "./App.css";
import { Switch, Route, useHistory, Redirect } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { Header, Footer, ProtectedRoute } from "./components";
import MetaTags from 'react-meta-tags';
import api from "./api";
import styles from "./styles.module.css";

import {
  Main,
  SignIn,
  SignUp,
  MoneyFlowCreate,
  ChangePassword,
  NotFound,
  UpdateAvatar,
} from "./pages";

import { AuthContext, UserContext } from "./contexts";
import MoneyFlowDetail from './pages/money-flow-detail';
import StatusList from './pages/status-list';
import TypeList from './pages/type-list';
import CategoryList from './pages/category-list';
import SubcategoryList from './pages/subcategory-list';
import MoneyFlowEdit from './pages/money-flow-edit';

function App() {
  const [loggedIn, setLoggedIn] = useState(null);
  const [user, setUser] = useState({});
  const [authError, setAuthError] = useState({ submitError: "" });
  const [registrError, setRegistrError] = useState({ submitError: "" });
  const [changePasswordError, setChangePasswordError] = useState({
    submitError: "",
  });

  const registration = ({
    email,
    password,
    username,
    first_name,
    last_name,
  }) => {
    api
      .signup({ email, password, username, first_name, last_name })
      .then(() => {
        history.push("/signin");
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          setRegistrError({ submitError: errors.join(", ") });
        }
        setLoggedIn(false);
      });
  };

  const changePassword = ({ new_password, current_password }) => {
    api
      .changePassword({ new_password, current_password })
      .then((res) => {
        history.push("/signin");
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          setChangePasswordError({ submitError: errors.join(", ") });
        }
      });
  };

  const changeAvatar = ({ file }) => {
    api
      .changeAvatar({ file })
      .then((res) => {
        setUser({ ...user, avatar: res.avatar });
        history.push(`/recipes`);
      })
      .catch((err) => {
        const { non_field_errors } = err;
        if (non_field_errors) {
          return alert(non_field_errors.join(", "));
        }
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(", "));
        }
      });
  };

  const authorization = ({ email, password }) => {
    api
      .signin({
        email,
        password,
      })
      .then((res) => {
        if (res.auth_token) {
          localStorage.setItem("token", res.auth_token);
          api
            .getUserData()
            .then((res) => {
              setUser(res);
              setLoggedIn(true);
            })
            .catch((err) => {
              setLoggedIn(false);
              history.push("/signin");
            });
        } else {
          setLoggedIn(false);
        }
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          setAuthError({ submitError: errors.join(", ") });
        }
        setLoggedIn(false);
      });
  };

  const onPasswordReset = ({ email }) => {
    api
      .resetPassword({
        email,
      })
      .then((res) => {
        history.push("/signin");
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(", "));
        }
        setLoggedIn(false);
      });
  };

  const loadSingleItem = ({ id, callback }) => {
    setTimeout((_) => {
      callback();
    }, 3000);
  };

  const history = useHistory();
  const onSignOut = () => {
    api
      .signout()
      .then((res) => {
        localStorage.removeItem("token");
        setLoggedIn(false);
      })
      .catch((err) => {
        const errors = Object.values(err);
        if (errors) {
          alert(errors.join(", "));
        }
      });
  };

  useEffect((_) => {
    const token = localStorage.getItem("token");
    if (token) {
      return api
        .getUserData()
        .then((res) => {
          setUser(res);
          setLoggedIn(true);
        })
        .catch((err) => {
          setLoggedIn(false);
          history.push("/recipes");
        });
    } else {
      setLoggedIn(false);
    }
  }, []);

  // useEffect(() => {
  //   document.addEventListener('keydown', function(event) {
  //     if (event.ctrlKey && event.shiftKey && event.key === 'z') {
  //       alert('зиги - добар пас!');
  //     }
  //   });
  // }, [])

  if (loggedIn === null) {
    return <div className={styles.loading}>Загрузка...</div>;
  }

  return (
    <AuthContext.Provider value={loggedIn}>
      <UserContext.Provider value={user}>
        <div className="App">
          <Header loggedIn={loggedIn} />
          <main className="main">
            <Switch>
              <Route exact path="/" component={Main} />
              <Route exact path="/signin" component={SignIn} />
              <Route exact path="/signup" component={SignUp} />
              
              <ProtectedRoute 
                exact 
                path="/money-flow-create" 
                component={MoneyFlowCreate}
                loggedIn={loggedIn}
              />
              <ProtectedRoute 
                exact 
                path="/money-flow/:id/edit" 
                component={MoneyFlowEdit}
                loggedIn={loggedIn}
              />
              <Route exact path="/money-flow/:id" component={MoneyFlowDetail} />
              
              <ProtectedRoute
                exact
                path="/change-password"
                component={ChangePassword}
                loggedIn={loggedIn}
                submitError={changePasswordError}
                setSubmitError={setChangePasswordError}
                onPasswordChange={changePassword}
              />

              <ProtectedRoute
                exact
                path="/change-avatar"
                component={UpdateAvatar}
                loggedIn={loggedIn}
                onAvatarChange={changeAvatar}
              />

              <Route exact path="/statuses" component={StatusList} />
              <Route exact path="/types" component={TypeList} />
              <Route exact path="/categories" component={CategoryList} />
              <Route exact path="/subcategories" component={SubcategoryList} />
              
              <Route path="*">
                <NotFound />
              </Route>
            </Switch>
          </main>
          <Footer />
        </div>
      </UserContext.Provider>
    </AuthContext.Provider>
  );
}

export default App;
