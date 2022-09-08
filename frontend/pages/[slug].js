import { Loader } from 'react-bulma-components'
import { useRouter } from "next/router";

export default function Post({ post }) {
  const router = useRouter()
  console.log(post)
  if (router.isFallback)
    return <div><Loader color='primary' textSize={1} /> Loading...</div>
  return (
    <div className='section content'>
      <h1>{post.title}</h1>
      <div>
        {post.body}
      </div>
    </div>
  )
}

export async function getStaticPaths() {
  // const res = await fetch('http://localhost:5000/')
  // const { posts } = await res.json()
  return {
    paths: [{ params: { slug: 'title-is-here' } }],
    fallback: false,
  }
}

export async function getStaticProps({ params }) {
  const res = await fetch(`http://localhost:5000/${params.slug}`, { mode: 'no-cors' })
  const post = await res.json()

  return {
    props: { post }
  }
}
