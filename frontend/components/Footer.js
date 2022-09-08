import { FaDiscord, FaEnvelope, FaFacebook, FaFly, FaMailBulk, FaTelegram, FaTwitter } from 'react-icons/fa';

export default function Footer() {
  return (
    <footer className="has-text-dark has-background-white  p-4">
      <div className="container">
        <div className="columns">
          <div className="column">
            <div className="menu">
              <div className="menu-label">Our Service</div>
              <ul className="menu-list">
                <li>
                  <a href="#">Meet Customer Service</a>
                </li>
                <li>
                  <a href="#">Send feedback</a>
                </li>
                <li>
                  <a href="#">Customer Service</a>
                </li>
                <li>
                  <a href="#">Our terms and agreements</a>
                </li>
              </ul>
            </div>
          </div>
          <div className="column">
            <div className="menu">
              <div className="menu-label">Spread the word</div>
            </div>
            <ul className='menu-label'>
              <li>
                <button className="button py-0 px-1 is-ghost">
                  <FaFacebook className="mr-1" /> Facebook
                </button>
              </li>
              <li>
                <button className="button py-0 px-1 is-ghost">
                  <FaTelegram className="mr-1" /> Telegram
                </button>
              </li>
              <li>
                <button className="button py-0 px-1 is-ghost">
                  <FaTwitter className="mr-1" /> Twitter
                </button>
              </li>
              <li>
                <button className="button py-0 px-1 is-ghost">
                  <FaDiscord className="mr-1" /> Discord
                </button>
              </li>
            </ul>
          </div>
          <div className='column is-3'>
            <div className='menu-label'>
              About us
            </div>
            <p>
              lorem ipsum sit amet doler
            </p>
          </div>
          <div className="column is-3">
            <div className='menu'>
              <div className='menu-label'>
                Leave us a message
              </div>
              <div className='menu-list'>
                <div className="field">
                  <p className="control has-icons-left">
                    <input className="input is-small" type="email" placeholder="Email" />
                    <span className="icon is-small is-left">
                      <FaEnvelope />
                    </span>
                  </p>
                </div>
                <div className='field'>
                  <textarea className='textarea is-small' rows='2' placeholder='message'></textarea>
                </div>
                <div className="field">
                  <div className="buttons is-right">
                    <button className="button is-small">
                      <FaEnvelope className='mr-2' />
                      send</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
        <p className="has-text-centered">
          Made with 💜 by <a href="https://github.com/dere7">dere7</a>
        </p>
      </div>
    </footer>
  );
}
