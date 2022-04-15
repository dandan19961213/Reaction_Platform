import React from 'react';
import OverPack from 'rc-scroll-anim/lib/ScrollOverPack';
import QueueAnim from 'rc-queue-anim';
import { getChildrenToRender } from './utils';
import {Row, Col} from 'antd';

class Content9 extends React.PureComponent {
  getBlockChildren = (block, i) => {
    const { isMobile } = this.props;
    const item = block.children;
    const imageWrapper = (
        <QueueAnim
          className="image-wrapper"
          key="image"
          type={isMobile ? 'right' : 'bottom'}
          leaveReverse
          delay={isMobile ? [100, 0] : 0}
          {...item.imgWrapper}
        >
          <div key="title_l_des" {...item.title_l_des}>
            {item.title_l_des.children}
          </div>
          <div key="title_l" {...item.title_l}>
            {item.title_l.children}
          </div>
        </QueueAnim>
    );
    const textWrapper = (
      <QueueAnim
        key="text"
        leaveReverse
        delay={isMobile ? [0, 100] : 0}
        {...item.textWrapper}
      >
      <div>
        <div key="title_r_des" {...item.title_r_des}>
          {item.title_r_des.children}
        </div>
        <div key="title_r" {...item.title_r}>
          {item.title_r.children}
        </div>
      </div>
      </QueueAnim>
    );
    return (
      <Row gutter={[50, 50]} justify="space-around" align="middle">
        <Col className="gutter-row" xs={24} sm={12} md={12} lg={12} xl={12} flex={1}>
          {imageWrapper}
        </Col>
        <Col className="gutter-row" xs={24} sm={12} md={12} lg={12} xl={12} flex={1}>
          {textWrapper}
        </Col>
      </Row>
    );
  };
  render() {
    const { ...props } = this.props;
    const { dataSource } = props;
    delete props.dataSource;
    delete props.isMobile;
    const children = dataSource.block.children.map(this.getBlockChildren);
    return (
      <div {...props} {...dataSource.wrapper}>
        <div {...dataSource.page}>
          <div {...dataSource.titleWrapper}>
            {dataSource.titleWrapper.children.map(getChildrenToRender)}
          </div>
          <div {...dataSource.block}>
            {children}
          </div>
        </div>
      </div>
    );
  }
}

export default Content9;
