import Head from 'next/head';
import Nav from '../components/Nav';
import { FaArrowAltCircleRight } from 'react-icons/fa'
import Card from '../components/Card';

export default function Home({ posts }) {
  return (
    <>
      <Head>
        <title>Blogy - Share your Idea</title>
        <meta name="description" content="Share your Idea" />
      </Head>
      <div className="hero is-dark" style={{
        backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("/graduation.jpg")',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
      }}>
        <div className="hero-head">
          <Nav />
        </div>
        <div className="hero-body container is-flex is-flex-direction-column is-justify-content-center is-align-items-center has-text-align-center">
          <h1 className="title is-1">
            Share your <em>IDEA/STORY</em> with Blogy
          </h1>
          <h2 className="subtitle is-3" style={{ maxWidth: "60ch" }}>
            We believe your STORY or IDEA is worth sharing. It make huge difference if we make those ideas and stories shared. Let's make knowledge free for everyone.
          </h2>
          <button className="button is-outlined is-medium is-light">
            GET STARTED
            <FaArrowAltCircleRight className='ml-2' />
          </button>
        </div>
      </div>
      <main className='container'>
        <div className="section">
          <div className="title is-3 m-2">Recent Posts</div>
          <div className="columns is-multiline">
            {posts.map((post, i) => <Card {...post} key={i} />)}
          </div>
          <nav className="pagination is-small is-rounded" role="navigation" aria-label="pagination">
            <a className="pagination-previous" disabled>Previous</a>
            <a className="pagination-next">Next page</a>
            <ul className="pagination-list">
              <li><a className="pagination-link" aria-label="Goto page 1">1</a></li>
              <li><span className="pagination-ellipsis">&hellip;</span></li>
              <li><a className="pagination-link" aria-label="Goto page 45">45</a></li>
              <li><a className="pagination-link is-current" aria-label="Page 46" aria-current="page">46</a></li>
              <li><a className="pagination-link" aria-label="Goto page 47">47</a></li>
              <li><span className="pagination-ellipsis">&hellip;</span></li>
              <li><a className="pagination-link" aria-label="Goto page 86">86</a></li>
            </ul>
          </nav>
        </div>
      </main>
    </>
  );
}

export async function getStaticProps() {
  const res = await fetch(process.env.API_URL)
  const { posts } = await res.json()
  return {
    props: {
      posts
    },
  }
}
