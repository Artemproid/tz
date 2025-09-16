import {
  Container,
  Input,
  FormTitle,
  Main,
  Form,
  Button,
} from "../../components";
import styles from "./styles.module.css";
import { useFormWithValidation } from "../../utils/validation";
import { Redirect } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../../contexts";
import MetaTags from "react-meta-tags";
import { useHistory } from "react-router-dom";
import api from "../../api";

const SignUp = () => {
  const [error, setError] = useState("");
  const history = useHistory();
  const { values, handleChange, errors, isValid, handleSubmit } = useFormWithValidation();
  const authContext = useContext(AuthContext);

  const onSubmit = async (data) => {
    try {
      await api.signup(data);
      history.push("/");
    } catch (err) {
      console.error('Ошибка при регистрации:', err);
      setError(err.message);
    }
  };

  return (
    <Main withBG asFlex>
      {authContext && <Redirect to="/" />}
      <Container className={styles.center}>
        <MetaTags>
          <title>Регистрация</title>
          <meta
            name="description"
            content="Создание аккаунта в системе учета финансов"
          />
          <meta property="og:title" content="Регистрация" />
        </MetaTags>
        <FormTitle>Регистрация</FormTitle>
        <Form
          className={styles.form}
          onSubmit={handleSubmit(onSubmit)}
        >
          <Input
            required
            label="Имя"
            name="first_name"
            onChange={handleChange}
            value={values.first_name || ""}
            error={errors.first_name}
          />
          <Input
            required
            label="Фамилия"
            name="last_name"
            onChange={handleChange}
            value={values.last_name || ""}
            error={errors.last_name}
          />
          <Input
            required
            label="Email"
            type="email"
            name="email"
            onChange={handleChange}
            value={values.email || ""}
            error={errors.email}
          />
          <Input
            required
            label="Логин"
            name="username"
            onChange={handleChange}
            value={values.username || ""}
            error={errors.username}
          />
          <Input
            required
            label="Пароль"
            type="password"
            name="password"
            onChange={handleChange}
            value={values.password || ""}
            error={errors.password}
          />
          <Button
            type="submit"
            disabled={!isValid}
          >
            Создать аккаунт
          </Button>
        </Form>
        {error && <p className={styles.error}>{error}</p>}
      </Container>
    </Main>
  );
};

export default SignUp;
