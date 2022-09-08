import Head from "next/head";
import Link from "next/link";
import { useRouter } from "next/router";
import { FaEnvelope, FaLock, FaUser } from "react-icons/fa";
import { Button, Form, Card, Heading, Icon } from "react-bulma-components";
import { useForm } from "react-hook-form";
import { useState } from "react";

export default function Signup() {

  const { register, handleSubmit, formState: { errors } } = useForm()
  const router = useRouter()
  const [error, setError] = useState(null)

  const onSubmit = async (data, e) => {
    e.preventDefault()
    const res = await fetch('http://localhost:5000/user/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })

    const response = await res.json()
    if (res.status === 201)
      router.push('/auth/login')
    else
      setError(JSON.stringify(response.error))
  }

  return (
    <>
      <Head>
        <title>Create Account - Blogy | Share your Idea</title>
        <meta name="description" content="Create account" />
      </Head>
      <div className="is-flex is-justify-content-center is-align-items-center" style={{ height: '100%' }}>
        <Card>
          <Card.Content className="has-text-centered">
            <Heading>Signup</Heading>
            <p className="subtitle">
              or <Link href="/auth/login">
                <a>already have account?</a>
              </Link>
            </p>
            {error && (<Form.Help textSize={6} color='danger' mb={3}>  {error}</Form.Help>)}
            <form onSubmit={handleSubmit(onSubmit)}>
              <Form.Field>
                <Form.Control className="has-icons-left">
                  <input
                    {...register('full_name', { required: true, min: 6 })}
                    className="input" type="text" placeholder="Full Name" />
                  <Icon size={"small"} align="left">
                    <FaUser />
                  </Icon>
                  <Form.Help textAlign={'left'}>* required</Form.Help>
                  {errors.full_name && (<Form.Help textAlign={'left'} color={'danger'}>require &ge; 6 characters</Form.Help>)}
                </Form.Control>
              </Form.Field>
              <Form.Field>
                <Form.Control className="has-icons-left">
                  <input
                    {...register('email', { required: true, pattern: /^\S+@\S+.\S+$/ })}
                    className="input" type="email" placeholder="Email" />
                  <Icon size={"small"} align="left">
                    <FaEnvelope />
                  </Icon>
                  <Form.Help textAlign={'left'}>* required</Form.Help>
                  {errors.email && (<Form.Help textAlign={'left'} color={'danger'}>Invalid email</Form.Help>)}
                </Form.Control>
              </Form.Field>
              <Form.Field>
                <Form.Control className="has-icons-left">
                  <input
                    {...register('password', { required: true, minLength: 6 })}
                    className="input" type="password" placeholder="Password" />
                  <Icon size={"small"} align="left">
                    <FaLock />
                  </Icon>
                  <Form.Help textAlign={'left'}>* requires &ge; 6 characters</Form.Help>
                  {errors.password && (<Form.Help textAlign={'left'} color={'danger'}>
                    password is required and must be &ge; 6 characters
                  </Form.Help>)}
                </Form.Control>
              </Form.Field>
              <Form.Field>
                <div className="buttons is-right">
                  <Button color={"primary"}>Sign up</Button>
                </div>
              </Form.Field>
            </form>
          </Card.Content>
        </Card>
      </div>
    </>
  )
}