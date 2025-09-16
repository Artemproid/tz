import styles from './styles.module.css'
import { Button } from '..'

const Popup = ({ children, onClose }) => {
  return <div className={styles.popup}>
    <div className={styles.popup__content}>
      <Button
        className={styles.popup__close}
        onClick={onClose}
      >
        ✕
      </Button>
      {children}
    </div>
  </div>
}

export default Popup