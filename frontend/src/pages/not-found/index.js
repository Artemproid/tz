import { Button, Container, Main } from "../../components";
import styles from "./styles.module.css";
import { useHistory } from "react-router-dom";

const NotFound = () => {
  const history = useHistory();

  return (
    <Main>
      <Container>
        <div className={styles.notFound}>
          <h1>404</h1>
          <p>Страница не найдена</p>
          <Button
            onClick={() => history.push("/")}
            className={styles.button}
          >
            Перейти на главную
          </Button>
        </div>
      </Container>
    </Main>
  );
};

export default NotFound;
