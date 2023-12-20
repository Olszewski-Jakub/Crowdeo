import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import GitHubButton from './GitHubButton';
const FeatureList = [
  {
    title: 'Panda',
    Image: '@site/static/img/Panda.png',
    description: (
      <>
        Panda is a device that is resposible for tracking amount of users in a specified area using BLE technology. It is based on Raspberry Pi Pico or ESP32 microcontroller.
      </>
    ),
    repoName: 'Panda',
    username: 'Olszewski-Jakub',
  },
  {
    title: 'Bamboo',
    description: (
      <>
        Bamboo is an API that makes evrything work together. It is responsible for storing data from Pandas and providing it to the users on Crowdeo Dashboard.
      </>
    ),
    repoName: 'Bamboo',
    username: 'Olszewski-Jakub',
  },
  {
    title: 'Crowdeo Dashboard',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Crowdeo Dashboard is a web application that provides you with all the data you need. It is based on React and is using Bamboo API to get the data.
      </>
    ),
    repoName: 'Crowdeo-Dashboard',
    username: 'Olszewski-Jakub',
  },
];

function Feature({Svg, title, description, repoName, username}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="card">
        <div className="card__body">
          <div className="text--center padding-horiz--md">
            <Heading as="h3">{title}</Heading>
            <p>{description}</p>
            <GitHubButton username={username} repoName={repoName} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
