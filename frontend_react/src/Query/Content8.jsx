import React from 'react';
import TweenOne from 'rc-tween-one';
import OverPack from 'rc-scroll-anim/lib/ScrollOverPack';
import { Row, Col} from 'antd';
import QueueAnim from 'rc-queue-anim';
import { getChildrenToRender } from './utils';

class Content8 extends React.PureComponent {
  render() {
    const { ...props } = this.props;
    const { dataSource } = props;
    delete props.dataSource;
    delete props.isMobile;
    // const children = dataSource.block.children.map(this.getBlockChildren);
    return (
      <div {...props} {...dataSource.wrapper}>
        <div {...dataSource.page}>
          <div {...dataSource.titleWrapper}>
            {dataSource.titleWrapper.children.map(getChildrenToRender)}
          </div>
          <div>
            <Row gutter={[16]} justify="space-around" align="middle">
              <Col className="gutter-row" xs={24} sm={12} md={12} lg={12} xl={12} flex={1}>
                <OverPack {...dataSource.OverPack}>
                  <QueueAnim type="bottom" key="img">
                    <Row {...dataSource.block} justify="center" key="img">
                      {/* {children} */}
                    </Row>
                  </QueueAnim>
                </OverPack>
              </Col>
            </Row>
          </div>
          <div>
            <Row>
              <Col span={6} offset={18}>
                <div {...dataSource.upWrapper}>
                  {dataSource.upWrapper.children.map(getChildrenToRender)}
                </div>
              </Col>
            </Row>
          </div>
        </div>
      </div>  
    );
  }
}

export default Content8;
