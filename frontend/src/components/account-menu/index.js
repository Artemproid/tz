import styles from './styles.module.css'
import { Button } from '..'

const AccountMenu = ({ onSignOut }) => {
  return <div className={styles.menu}>
    <Button
      className={styles.button}
      onClick={onSignOut}
    >
      Выйти
    </Button>
  </div>
}

export default AccountMenu