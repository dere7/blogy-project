import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from "next/router";
import { useState } from 'react';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import { Button, Form, Card, Heading, Icon } from "react-bulma-components";
import { useForm } from "react-hook-form";


export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm()
  const router = useRouter()
  const [error, setError] = useState(null)

  const onSubmit = async (data, e) => {
    e.preventDefault()
    const res = await fetch('http://localhost:5000/user/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    const response = await res.json()
    if (res.status === 200) {
      localStorage.setItem('token', response.token);
      router.push('/')
    } else
      setError(JSON.stringify(response.error))
  }

  return (
    <>
      <Head>
        <title>Login - Blogy | Share your Idea</title>
        <meta name="description" content="Share your Idea" />
      </Head>
      <div
        className="is-flex is-justify-content-center is-align-items-center"
        style={{ height: '100%' }}
      >
        <Card>
          <Card.Content className="has-text-centered">
            <Heading>Login</Heading>
            <p className="subtitle">
              or{' '}
              <Link href="/auth/signup">
                <a>create new account</a>
              </Link>
            </p>
            {error && (<Form.Help textSize={6} color='danger' mb={3}>  {error}</Form.Help>)}
            <form onSubmit={handleSubmit(onSubmit)}>
              <Form.Field>
                <Form.Control className="has-icons-left">
                  <input className='input'
                    {...register('email', { required: true, pattern: /^\S+@\S+.\S+$/ })}
                    type="email"
                    placeholder="Email"
                  />
                  <Icon size={'small'} align='left'>
                    <FaEnvelope />
                  </Icon>
                </Form.Control>
                <Form.Help textAlign={'left'}>* required</Form.Help>
                {errors.email && (<Form.Help textAlign={'left'} color={'danger'}>Invalid email</Form.Help>)}
              </Form.Field>
              <Form.Field>
                <Form.Control className="has-icons-left">
                  <input className='input'
                    {...register('password', { required: true, minLength: 6 })}
                    type="password"
                    placeholder="Password"
                  />
                  <Icon size={'small'} align='left'>
                    <FaLock />
                  </Icon>
                </Form.Control>
                <Form.Help textAlign={'left'}>* requires &ge; 6 characters</Form.Help>
                {errors.password && (<Form.Help textAlign={'left'} color={'danger'}>
                  password is required and must be &ge; 6 characters
                </Form.Help>)}
              </Form.Field>
              <Form.Field>
                <div className="buttons is-right">
                  <Button color={'primary'}>Login</Button>
                </div>
              </Form.Field>
            </form>
          </Card.Content>
        </Card>
      </div>
    </>
  );
}
