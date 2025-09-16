import React from "react";
import styles from "./styles.module.css";
import { Button } from "..";

const Account = ({ onSignOut }) => {
  return (
    <div className={styles.menu}>
      <Button
        className={styles.button}
        onClick={onSignOut}
      >
        Выйти
      </Button>
    </div>
  );
};

export default Account;
