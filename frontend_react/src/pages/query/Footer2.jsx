import React from 'react';
import TweenOne from 'rc-tween-one';
import OverPack from 'rc-scroll-anim/lib/ScrollOverPack';
import { isImg } from './utils';
import { Row, Col} from 'antd';

class Footer2 extends React.PureComponent {
  render() {
    const { ...props } = this.props;
    const { dataSource } = props;
    delete props.dataSource;
    delete props.isMobile;
    return (
      <Row>
        <Col className="gutter-row" xs={24} sm={24} md={24} lg={24} xl={24} flex={24}>
        <div {...props} {...dataSource.wrapper}>
          <OverPack {...dataSource.OverPack}>
            <TweenOne {...dataSource.links}>
              {dataSource.links.children.map((item, i) => {
                return (
                  <a key={i.toString()} {...item}>
                    <img src={item.children} height="100%" alt="img" />
                  </a>
                );
              })}
            </TweenOne>
            <TweenOne
              animation={{ x: '+=30', opacity: 0, type: 'from' }}
              key="copyright"
              {...dataSource.copyright}
            >
              {dataSource.copyright.children.map((item, i) =>
                React.createElement(
                  item.name.indexOf('title') === 0 ? 'h1' : 'div',
                  { key: i.toString(), ...item },
                  typeof item.children === 'string' && item.children.match(isImg)
                    ? React.createElement('img', {
                        src: item.children,
                        alt: 'img',
                      })
                    : item.children
                )
              )}
            </TweenOne>
          </OverPack>
        </div>
        </Col>
      </Row>
      
    );
  }
}

export default Footer2;
