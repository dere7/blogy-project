import 'bulma/css/bulma.min.css'
import Layout from '../components/Layout'
import '../styles/global.css'

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}

export default MyApp
