import Link from "next/link"

export default function Card({ author, title, body, slug }) {
  return (
    <div className="column is-4-desktop is-6-tablet">
      <div className="card">
        <div className="card-image">
          <figure className="imageis-4by3">
            <img src="/graduation.jpg" alt="" />
          </figure>
        </div>
        <div className="card-content">
          <div className="media">
            <div className="media-left">
              <figure className="image is-round is-48x48">
                <img src="/128x128.png" className="is-round" alt="Placeholder image" />
              </figure>
            </div>
            <div className="media-content">
              <p className="title is-4">{author.full_name}</p>
              <p className="subtitle is-6">{author.email}</p>
            </div>
          </div>

          <div className="content">
            <h3>{title}</h3>
            <p>
              {body}
              <Link href={`/${slug}`}>
                <a>see more ↬ </a>
              </Link>

            </p>
          </div>
        </div>
      </div >
    </div >)
}