import Head from "next/head";
import { useRouter } from "next/router";
import Footer from "./Footer";
import Nav from "./Nav";

export default function Layout({ children, isHome }) {
  const router = useRouter()
  return (
    <div className='has-background-light'>
      <Head>
        <title>Login - Blogy | Share your Idea</title>
        <meta name="description" content="Share your Idea" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {router.pathname == '/' ? children : (
        <>
          <Nav />
          <main style={{ height: "calc(100vh - 56px - 254px)" }}>
            {children}
          </main>
        </>
      )}
      <Footer />
    </div>
  )
}
