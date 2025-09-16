import styles from './styles.module.css'
import cn from 'classnames'

const Form = ({ children, className, onSubmit }) => {
  return <form
    className={cn(styles.form, className)}
    onSubmit={onSubmit}
  >
    {children}
  </form>
}

export default Form
