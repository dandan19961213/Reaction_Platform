import React from 'react';
import OverPack from 'rc-scroll-anim/lib/ScrollOverPack';
import QueueAnim from 'rc-queue-anim';
import { getChildrenToRender } from './utils';

class Content9 extends React.PureComponent {
  getBlockChildren = (block, i) => {
    const { isMobile } = this.props;
    const item = block.children;
    const textWrapper = (
      <QueueAnim
        key="text"
        leaveReverse
        delay={isMobile ? [0, 100] : 0}
        {...item.textWrapper}
      >
        <div key="title_r_des" {...item.title_r_des}>
          {item.title_r_des.children}
        </div>
        <div key="title_r" {...item.title_r}>
          {item.title_r.children}
        </div>
      </QueueAnim>
    );
    return (
      <OverPack key={i.toString()} {...block}>
        {isMobile && textWrapper}

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
        {!isMobile && textWrapper}
      </OverPack>
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
          <div {...dataSource.block}>{children}</div>
        </div>
      </div>
    );
  }
}

export default Content9;
