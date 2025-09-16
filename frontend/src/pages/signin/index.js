import React from 'react';
import { useHistory } from 'react-router-dom';
import {
  Container,
  Input,
  Main,
  Form,
  Button,
  FormTitle,
} from "../../components";
import styles from "./styles.module.css";
import { useFormWithValidation } from "../../utils";
import { AuthContext } from "../../contexts";
import { Redirect } from "react-router-dom";
import { useContext } from "react";
import MetaTags from "react-meta-tags";
import api from '../../api';

const SignIn = () => {
  const { values, handleChange, errors } = useFormWithValidation();
  const authContext = useContext(AuthContext);
  const [error, setError] = React.useState('');
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.signin(values);
      if (response.auth_token) {
        localStorage.setItem('token', response.auth_token);
        window.location.reload();
      }
    } catch (err) {
      setError('Неверный логин или пароль');
    }
  };

  return (
    <Main withBG asFlex>
      {authContext && <Redirect to="/" />}
      <Container className={styles.container}>
        <Form className={styles.form} onSubmit={handleSubmit}>
          <FormTitle>Войти</FormTitle>
          <Input
            name="email"
            type="email"
            placeholder="Email"
            value={values.email || ''}
            onChange={handleChange}
            error={errors.email}
          />
          <Input
            name="password"
            type="password"
            placeholder="Пароль"
            value={values.password || ''}
            onChange={handleChange}
            error={errors.password}
          />
          {error && <p className={styles.error}>{error}</p>}
          <Button type="submit">Войти</Button>
        </Form>
      </Container>
    </Main>
  );
};

export default SignIn;
