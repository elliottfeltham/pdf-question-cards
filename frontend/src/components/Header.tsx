import styles from "./Header.module.css";

type HeaderProps = {
	title: string;
};

const Header = ({ title }: HeaderProps) => {
	return <div className={styles.header}>{title}</div>;
};

export default Header;
