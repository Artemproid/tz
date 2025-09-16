import styles from './styles.module.css'

const FileInput = ({ onChange, file, className }) => {
  const handleChange = (e) => {
    const file = e.target.files[0]
    onChange(file)
  }

  return <div className={styles.container}>
    <input
      type='file'
      onChange={handleChange}
      className={styles.input}
    />
    {file && <button
      className={styles.delete}
      onClick={() => onChange(null)}
    >
      Удалить
    </button>}
  </div>
}

export default FileInput