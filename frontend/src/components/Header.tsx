import styles from "./Header.module.css";

type HeaderProps = {
	title: string;
};

const Header = ({ title }: HeaderProps) => {
	return (
		<header className={styles.header}>
			<h1 className={styles.title}>{title}</h1>
			<p className={styles.subheading}>
				Convert any PDF document into a set of question cards!
			</p>
		</header>
	);
};

export default Header;
